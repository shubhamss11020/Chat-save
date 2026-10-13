---
conversation_id: deefebac-7068-4d9d-a08b-9a29b62d2b9b
platform: claude
username: "harsh"
title: "Cloud platform infrastructure pricing comparison - Claude"
created_at: "2026-10-13 09:23:56 EDT"
updated_at: "2026-10-13 09:27:27 EDT"
---

# Cloud platform infrastructure pricing comparison - Claude

## User (2026-10-13 09:23:07 EDT)

Give me detail about all the cost infra level specs for aws/render/railway/digital ocean etc.. and one two or all

## Claude (2026-10-13 09:23:56 EDT)

Short version: the four platforms bill in different ways. Render charges a flat price per service, Railway meters the CPU and RAM you actually use, DigitalOcean sells fixed-size servers (Droplets) plus add-ons, and AWS charges per resource with many small extras. Prices below are USD from public pages and third-party trackers dated mid-2026, so confirm them on each vendor’s pricing page before you commit.

Render (flat price per service)
Web Service Starter is $7/mo (0.5 CPU, 512 MB) and Standard is $25/mo (1 CPU, 2 GB). Higher tiers are Pro $85, Pro Plus $175, Pro Max $225 and Pro Ultra $450 per month. 
jwatte
livemy
Workspace plans are Hobby $0, Pro $25/month and Scale $499/month, plus compute for every service. One source instead lists Professional at $19 per user, so check which applies to you. 
temps
devcloudsoftware
Postgres starts around $6–7 and Redis around $10, each billed as its own service. A worker or cron job is also a separate line item. 
devcloudsoftware
Free web services spin down after 15 minutes without traffic, and waking up takes about a minute. 
jwatte
Workflow tasks are billed per run at $0.05/hour for 0.5 CPU/512 MB and $0.20/hour for 1 CPU/2 GB. 
onrender
Railway (usage-metered)
Hobby is $5/month and includes $5 of usage. Pro is $20/month and includes $20 of usage. One source says Pro is priced per workspace, not per seat, while others say per seat. Verify this before budgeting for a team. 
railway
temps
Rates are $20 per vCPU/month, $10 per GB of RAM/month, $0.05 per GB of egress and $0.15 per GB/month of volume storage, metered per second. Some third-party sites list $0.10/GB egress and $0.25/GB storage, but Railway’s own docs say $0.05 and $0.15. 
temps
A service holding 1 vCPU and 1 GB of RAM around the clock costs about $30/month in resources. 
temps
Per-service limits by plan:
Free: up to 1 vCPU / 0.5 GB. 
costbench
Hobby: up to 48 vCPU / 48 GB. 
costbench
Pro: up to 1,000 vCPU / 1 TB. 
costbench
Enterprise: up to 2,400 vCPU / 2.4 TB. 
costbench
DigitalOcean (fixed Droplets plus add-ons)
Basic Droplets start at $4/month for 1 vCPU, 512 MB RAM, 10 GB SSD and 500 GB transfer, and the Basic range tops out at $48/month for 8 GB. General Purpose starts at $63/month. CPU-Optimized starts at $42/month and Memory-Optimized at $84/month. 
www.temperstack.com +2
Managed Databases start at $15/month for Postgres or MySQL, and Redis starts at $25. The Redis figure comes from an older tracker. 
temperstack
App Platform is free for static sites and from $5/month for dynamic apps. 
temperstack
The Kubernetes control plane is effectively free, and you pay for worker nodes at normal Droplet rates. 
temperstack
Backups cost 20% of the Droplet price weekly or 30% daily, and bandwidth overage is $0.01/GiB. A load balancer is about $12/month. 
linuxteck
temperstack
AWS (per-resource, many add-ons)
EC2 Graviton instances are the cheapest: t4g.nano is $0.0042/hr and t4g.micro is $0.0084/hr, versus $0.0052 and $0.0104 for the x86 t3 equivalents. 
mgt-commerce
RDS Postgres/MySQL (us-east-1, single-AZ, on-demand):
db.t4g.micro (2 vCPU, 1 GiB) is about $11.68/month. 
holori
db.t4g.small (2 vCPU, 2 GiB) is about $23.36/month. 
holori
db.t4g.xlarge (4 vCPU, 16 GiB) is about $188/month. 
holori
db.m7g.large (2 vCPU, 8 GiB) is about $123/month. 
bytebase
Storage, backups and IOPS cost extra.
The usual surprises:
A NAT Gateway costs $0.045/hour plus $0.045/GB processed in us-east-1. That is roughly $32/month while idle. 
computingforgeeks
Every public IPv4 address costs $0.005/hour, about $3.60/month. 
computingforgeeks
An EKS control plane is $0.10/hour, about $73/month per cluster. 
computingforgeeks
Data transfer out is $0.09/GB after the first 100 GB free each month. 
mgt-commerce
The old 12-month free tier only applies to accounts opened before July 15, 2025. Newer accounts get a different credit-based program that I didn’t verify. 
computingforgeeks
Reserved or savings-plan commitments cut compute costs considerably. For example, db.t4g.xlarge drops from $188 to about $126 per month on a 1-year reservation. 
bytebase
Rough “small production app” comparison

These are sourced examples, not like-for-like benchmarks.

Platform	Typical small stack	Approx. monthly
Render	$7 web service + $6 Postgres (256 MB)	$13
Render (heavier)	Standard web ($25) + Starter worker ($7) + Pro workspace ($25) + Postgres	$57 + Postgres
Railway	1 vCPU / 1 GB service plus plan fee, DB extra	about $30+
DigitalOcean	$12 Droplet + $15 managed DB + $12 load balancer	$39
AWS	No sourced total. Add the RDS micro (about $12) to an EC2 instance, then NAT, IPv4 and egress charges.	varies widely 
Render Pricing 2026: Free Tier Sleep, Plans, Compute +3
Which to pick
Render: best for predictable bills and a simple deploy workflow. It gets pricey as your service count and team seats grow.
Railway: best for bursty or low-traffic apps, since idle services cost little. Bills are less predictable under sustained load.
DigitalOcean: best price-to-spec for steady workloads. You manage more yourself if you use Droplets.
AWS: best when you need compliance, multi-region setups or deep services. It is the hardest to estimate and needs the most cost hygiene.

If you tell me your workload (services, traffic, database size, team size), I can build an estimate on two or three of these.

One note on archiving: this chat couldn’t be saved to the team archive. The save tool isn’t connected in this session, so check that connector in Settings → Connectors.
