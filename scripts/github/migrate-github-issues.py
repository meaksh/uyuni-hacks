#!/usr/bin/python3
#
# Script to migrate GitHub issues with a specific label from one repository
# to a different one which can be in a different organization.
# The script will copy labels, comments and preserve assignees and projectV2.
#
# Author: Pablo Suárez Hernández <psuarezhernandez@suse.com>
#

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

import argparse

#####################################################################

# GitHub Auth Token
# Required permissions: public_repo, project (full access)
AUTH_TOKEN = ""

# Source organization and repo to collect issues to migrate
SOURCE_ORG = "meaksh"
SOURCE_REPO = "test-repo-1"

# Target organization and repo where issues are going to be created
TARGET_ORG = "meaksh"
TARGET_REPO = "test-repo-2"

# The name of the label of issues to be migrated
MIGRATION_LABEL = "migrate-to-uyuni"

#####################################################################

parser = argparse.ArgumentParser(
    description="Migrate GitHub issues with a selected label to a different repository"
)
parser.add_argument("--migrate", action="store_true", help="Run the actual migration")
args = parser.parse_args()

# Prepare client for GitHub GraphQL API
transport = AIOHTTPTransport(
    url="https://api.github.com/graphql",
    headers={
        "Authorization": f"bearer {AUTH_TOKEN}",
        "Accept": "application/vnd.github.bane-preview+json",
    },
)
client = Client(transport=transport, fetch_schema_from_transport=True)

get_issues_to_migrate_query = gql(
    """
query getIssuesWithComments($owner: String!, $repo: String!, $migration_label: String!) {
  repository(owner: $owner, name: $repo) {
     id
     issues(first: 50, labels: [$migration_label], states: OPEN) {
       nodes {
         id
         title
         body
         number
         url
         createdAt
         assignees(last: 30) {
           nodes {
             id
           }
         }
         author {
           login
         }
         labels(first: 20) {
           nodes {
             name
             description
             color
           }
         }
         projectsV2(first: 10) {
           nodes {
             field(name: "Status") {
               ... on ProjectV2SingleSelectField {
                 id
               }
             }
           }
         }
         projectItems(first: 10) {
           nodes {
             project {
               title 
               id
             }
             id
             fieldValueByName(name: "Status") {
               ... on ProjectV2ItemFieldSingleSelectValue {
                 name
                 id
               }
             }
           }
         }
         comments(first: 50) {
           nodes {
             body
             author {
               login
             }
             createdAt
           }
         }
       }
     }
   }
}
"""
)

get_project_field_id_query = gql(
    """
query getProjectFieldFromIssue($project_id: ID!) {
  node(id:$project_id) {
    ... on ProjectV2 {
      field(name: "Status") {
        ... on ProjectV2SingleSelectField {
          id
          options {
            id
            name
          }
        }
      }
    }
  }
}
"""
)

get_label_from_repo_query = gql(
    """
query getLabelFromRepo($owner: String!, $repo: String!, $label: String!) {
  repository(owner: $owner, name: $repo) {
    label(name: $label) {
        id
        name
        description
        color
    }
    id
  }
}
"""
)

get_repository_id_query = gql(
    """
query getRepositoryId($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    id
  }
}
"""
)

create_label_mutation = gql(
    """
mutation($repo_id: ID!, $name: String!, $color: String!) {
  createLabel(input:{repositoryId:$repo_id,name:$name,color:$color}) {
    label {
      id
      name
    }
  }
}
"""
)

add_label_to_issue_mutation = gql(
    """
mutation($labelable_id: ID!, $label_ids: [ID!]!) {
  addLabelsToLabelable(input:{labelableId:$labelable_id,labelIds:$label_ids}) {
    labelable
  }
}
"""
)

add_assignee_to_issue_mutation = gql(
    """
mutation($assignable_id: ID!, $assignee_list: [ID!]!) {
  addAssigneesToAssignable(input:{assignableId:$assignable_id,assigneeIds:$assignee_list}) {
    assignable {
      assignees(last: 30) {
        nodes {
          id
        }
      }
    }
  }
}
"""
)

create_issue_mutation = gql(
    """
mutation($repo_id: ID!, $title: String!, $body: String!, $labelIds: [ID!]) {
  createIssue(input:{repositoryId:$repo_id,title:$title,body:$body,labelIds:$labelIds}) {
    issue {
      id
      title
      number
      url
    }
  }
}
"""
)

link_issue_mutation = gql(
    """
mutation($issue_id: ID!, $project_id: ID!) {
  addProjectV2ItemById(input:{contentId:$issue_id,projectId:$project_id}) {
    item {
      id
    }
  }
}
"""
)

close_issue_mutation = gql(
    """
mutation($issue_id: ID!, $state_reason: IssueClosedStateReason!) {
  closeIssue(input:{issueId:$issue_id,stateReason:$state_reason}) {
    issue {
      id
      url
    }
  }
}
"""
)

set_status_issue_mutation = gql(
    """
mutation($project_id: ID!, $item_id: ID!, $field_id: ID!, $value: ProjectV2FieldValue!) {
  updateProjectV2ItemFieldValue(input:{fieldId:$field_id,itemId:$item_id,projectId:$project_id,value:$value}) {
    projectV2Item {
      id
    }
  }
}
"""
)

add_comment_to_issue_mutation = gql(
    """
mutation($issue_id: ID!, $body: String!) {
  addComment(input:{subjectId:$issue_id,body:$body}) {
    subject {
      id
    }
  }
}
"""
)

create_project_field_mutation = gql(
    """
mutation($project_id: ID!, $name: String!, $data_type: ProjectV2CustomFieldType!) {
  createProjectV2Field(input:{projectId:$project_id,name:$name,dataType:$data_type}) {
    projectV2Field {
      ... on ProjectV2SingleSelectField {
        id
      }
    }
  }
}
"""
)

params = {
    "owner": SOURCE_ORG,
    "repo": SOURCE_REPO,
    "migration_label": MIGRATION_LABEL,
}

print("####################################")
print(
    "Looking for issue to migrate in '{}/{}' repository...".format(
        SOURCE_ORG, SOURCE_REPO
    )
)

# Check for issues to be migrated
issues_to_migrate = client.execute(get_issues_to_migrate_query, variable_values=params)
issues = issues_to_migrate["repository"]["issues"]["nodes"]

if not issues:
    print(
        "No issues with label '{}' in '{}/{}' source repository. Nothing to do.".format(
            MIGRATION_LABEL, SOURCE_ORG, SOURCE_REPO
        )
    )
    print("####################################")
    exit(0)

print("The following issues were detected to be migrated")
for issue in issues:
    comments = issue["comments"]["nodes"]
    print("####################################")
    print(
        "Issue title: {} | Creator: {}".format(issue["title"], issue["author"]["login"])
    )
    print("URL: {}".format(issue["url"]))
    print(
        "Issue labels: {}".format([label["name"] for label in issue["labels"]["nodes"]])
    )
    projects = issue["projectItems"]["nodes"]
    if projects:
        print("Projects:")
        for project in projects:
            print(
                " - {} -> {}".format(
                    project["project"]["title"],
                    project["fieldValueByName"] and project["fieldValueByName"]["name"],
                )
            )
    if comments:
        print("Number of comments: {}".format(len(comments)))

print("####################################")

if not args.migrate:
    print("Migration was not triggered. Use --migrate to run the migration")
    exit(0)

print()
print("Performing the migration")
print()

for issue in issues:
    try:
        print("####################################")
        print("# Copying issue: {}".format(issue["title"]))
        label_ids = []
        comments = issue["comments"]["nodes"]

        # First we copy labels that are not in the target repo
        print("# --- Copy labels")
        for label in issue["labels"]["nodes"]:
            # Exclude squad labels
            if "squad" in label["name"]:
                continue

            # Check if label exist on target repo.
            # if not existing, then create it
            params = {"owner": TARGET_ORG, "repo": TARGET_REPO, "label": label["name"]}
            target_label = client.execute(
                get_label_from_repo_query, variable_values=params
            )
            if not target_label["repository"]["label"]:
                new_label = client.execute(
                    create_label_mutation,
                    variable_values={
                        "repo_id": target_label["repository"]["id"],
                        "name": label["name"],
                        "color": label["color"],
                    },
                )
                print("Created missing label on repo: {}".format(label["name"]))
                label_ids.append(new_label["createLabel"]["label"]["id"])
            else:
                label_ids.append(target_label["repository"]["label"]["id"])

        # Get the target repository id
        repo_id = client.execute(
            get_repository_id_query,
            variable_values={"owner": TARGET_ORG, "repo": TARGET_REPO},
        )["repository"]["id"]

        # Then we create the issue in the target repo
        print("# --- Create issue")
        new_body = """
Issue created by automation script. Original author: @{} Date: {}
Source issue: {}

---
{}
""".format(
            issue["author"]["login"], issue["createdAt"], issue["url"], issue["body"]
        )
        new_issue = client.execute(
            create_issue_mutation,
            variable_values={
                "repo_id": repo_id,
                "title": issue["title"],
                "body": new_body,
                "labelIds": label_ids,
            },
        )
        new_issue_id = new_issue["createIssue"]["issue"]["id"]
        new_issue_number = new_issue["createIssue"]["issue"]["number"]
        print(
            "# ----- New issue created: {}".format(
                new_issue["createIssue"]["issue"]["url"]
            )
        )

        # Set the assignees to the new issue
        client.execute(
            add_assignee_to_issue_mutation,
            variable_values={
                "assignable_id": new_issue_id,
                "assignee_list": [x["id"] for x in issue["assignees"]["nodes"]],
            },
        )

        # Copy existing comments
        if not comments:
            print("# --- This issue has no comments")
        for comment in comments:
            new_body = """
Comment created by automation script. Original author: @{}. Date: {}

---
{}
""".format(
                comment["author"]["login"], comment["createdAt"], comment["body"]
            )
            client.execute(
                add_comment_to_issue_mutation,
                variable_values={"issue_id": new_issue_id, "body": new_body},
            )

        print("# --- Link issue to project")
        for project in issue["projectItems"]["nodes"]:
            # Link the new issue to board
            project_id = project["project"]["id"]
            new_item = client.execute(
                link_issue_mutation,
                variable_values={"issue_id": new_issue_id, "project_id": project_id},
            )
            new_item_id = new_item["addProjectV2ItemById"]["item"]["id"]

            # Set proper status for issue in project
            if project["fieldValueByName"]:
                # Get Project Status Field to modify
                new_field_id = client.execute(
                    get_project_field_id_query,
                    variable_values={"project_id": project_id},
                )

                client.execute(
                    set_status_issue_mutation,
                    variable_values={
                        "field_id": new_field_id["node"]["field"]["id"],
                        "value": {
                            "singleSelectOptionId": [
                                x
                                for x in new_field_id["node"]["field"]["options"]
                                if x["name"] == project["fieldValueByName"]["name"]
                            ][0]["id"]
                        },
                        "item_id": new_item_id,
                        "project_id": project["project"]["id"],
                    },
                )

        # Now, close source issue
        print("# --- Close old issue after migration is done")
        client.execute(
            close_issue_mutation,
            variable_values={
                "issue_id": issue["id"],
                "state_reason": "NOT_PLANNED",
            },
        )
    except Exception as exc:
        print("!!! ERROR while processing issue: {}".format(issue))
        print("{}".format(exc))

print("####################################")
