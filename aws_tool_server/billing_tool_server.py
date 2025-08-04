from fastapi import FastAPI
from pydantic import BaseModel
import boto3
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

class BillingQuery(BaseModel):
    service: str
    region: Optional[str] = None
    start_date: str
    end_date: str

@app.post("/get_aws_billing_costs")
def get_costs(query: BillingQuery):
    ce = boto3.client('ce', region_name='us-east-1')

    filters = [{"Dimensions": {"Key": "SERVICE", "Values": [query.service]}}]
    if query.region:
        filters.append({"Dimensions": {"Key": "REGION", "Values": [query.region]}})

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': query.start_date, 'End': query.end_date},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        Filter={"And": filters}
    )

    amount = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    return {
        "service": query.service,
        "region": query.region or "All",
        "start_date": query.start_date,
        "end_date": query.end_date,
        "cost": f"${float(amount):.2f}"
    }
