import boto3
from datetime import datetime, timedelta

# Initialize EC2 client
ec2 = boto3.client("ec2")

# Set retention period
RETENTION_DAYS = 30

def lambda_handler(event, context):
    volume_id = "vol-00beb917e98bb8635"  # Replace with your actual Volume ID

    # Step 1: Create a new EBS Snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=volume_id,
        Description=f"Automated Backup {datetime.now().strftime('%Y-%m-%d')}"
    )
    print(f"Snapshot created: {snapshot['SnapshotId']}")

    # Step 2: List and delete snapshots older than retention period
    snapshots = ec2.describe_snapshots(Filters=[{"Name": "volume-id", "Values": [volume_id]}])

    deletion_time = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

    for snap in snapshots["Snapshots"]:
        snapshot_id = snap["SnapshotId"]
        start_time = snap["StartTime"].replace(tzinfo=None)

        if start_time < deletion_time:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted old snapshot: {snapshot_id}")
