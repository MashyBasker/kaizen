from codecheck.helpers import output, parser
from codecheck.llms.provider import chat_completion
from codecheck.llms.prompts import CODE_REVIEW_PROMPT, CODE_REVIEW_SYSTEM_PROMPT
import requests


def review_pull_request(
    comment_url: str,
    diff_text: str,
    access_token: str,
    pull_request_title: str,
    pull_request_desc: str,
):

    prompt = CODE_REVIEW_PROMPT.format(
        PULL_REQUEST_TITLE=pull_request_title,
        PULL_REQUEST_DESC=pull_request_desc,
        CODE_DIFF=diff_text,
    )

    resp = chat_completion(
        prompt,
        system_prompt=CODE_REVIEW_SYSTEM_PROMPT,
    )

    body = output.json_to_markdown(parser.extract_json(resp))

    # Share the review on pull request
    post_pull_request(comment_url, body, access_token)


def post_pull_request(url, data, access_token):
    data = {
        "body": f"## Here is my AI generated review.\n \
            {data}\n\n -- Generated by Cloud Code AI"
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(url, headers=headers, json=data)
    print("Post Pull request response: ", response.text)
