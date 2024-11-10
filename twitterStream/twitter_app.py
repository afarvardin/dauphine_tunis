import socket
import requests
import json
import os

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHjUlAEAAAAAE%2BI4NVMiHWuxacTm6Yk2PBpTXUY%3Dyz3wwTt4NJRm8wgBj9s0S2E6zVqqGNtb1pvkQauemVsWoGNfsX'
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(
                response.status_code, response.text)
        )
    print("get_rules", json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print("delete_all_rules: ", json.dumps(response.json()))


def set_rules():
    # You can adjust the rules if needed
    sample_rules = [
        # {"value": "", "tags": ""} , YOU CAN APPLY UP TO 5 RULES PER REQUEST
        # {"value": "Tunisia lang:ar", "tag": "tweet about tunisia in arabic language"},
        {"value": "#inflation", "tag": "-"}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(
                response.status_code, response.text)
        )
    print("set_rules", json.dumps(response.json()))


def get_stream():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(f'status_code: {response.status_code}')
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    return response


def send_tweets_to_spark(tweets, tcp_connection):
    counter = 0
    for tweet in tweets.iter_lines():
        if tweet:
            full_tweet = json.loads(tweet)
            tweet_text = full_tweet.get('data')['text']
            print( tweet_text)
            print(f"------------------- {len(tweet_text)} -----------------------")
            tcp_connection.send(bytes(tweet_text, 'utf-8'))
            # tcp_connection.send(tweet_text)

def main():

    rules = get_rules()
    delete_all_rules(rules)
    set_rules()

    TCP_IP = "127.0.0.1"
    TCP_PORT = 9009
    conn = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)

    print("Waiting for TCP connection...")
    conn, addr = s.accept()

    print("Connected... Starting getting tweets.")

    tweets = get_stream()
    send_tweets_to_spark(tweets, conn)


if __name__ == "__main__":
    main()
