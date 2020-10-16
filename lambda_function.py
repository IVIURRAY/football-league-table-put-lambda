import csv
import json

import boto3


def lambda_handler(event, context):
    league = event["league"]
    user = event["user"]
    prediction = json.loads(event["table"])
    s3_bucket = "football-table-predictor-dev"
    s3_key = f"{league}/{user.lower()}_table.csv"

    output_file = f'/tmp/{user.lower()}_table.csv'
    with open(output_file, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["team", "rank"])
        writer.writeheader()
        writer.writerows(prediction)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)
    bucket.upload_file(output_file, s3_key)
    print(f"Uploaded to {s3_key}")


if __name__ == '__main__':
    print(lambda_handler({
        "league": "en1",
        "user": "haydn",
        "table": json.dumps([
            {"team": "Fulham FC", "rank": 1},
            {"team": "Arsenal FC", "rank": 3},
            {"team": "Crystal Palace FC", "rank": 2}
        ])
    }, None))
