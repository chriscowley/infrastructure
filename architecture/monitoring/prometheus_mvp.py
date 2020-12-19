#!/usr/bin/env python

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.general import General
from diagrams.aws.network import ELB
from diagrams.onprem.compute import Server
from diagrams.onprem.iac import Ansible
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import HAProxy
from diagrams.saas.alerting import Pushover
from diagrams.saas.chat import Slack

graph_attr = {
        }

node_attr = {
        }

with Diagram("Prometheus MVP",
             show=True,
             direction="TB",
             outformat="png",
             graph_attr=graph_attr,
             node_attr=node_attr):

    with Cluster("Rocky VPC"):
        with Cluster("Dashboard"):
            dashboard = Grafana("dashboards")
            loadbalancer = HAProxy("grfana")
            dashboard >> loadbalancer

        with Cluster("metrics cluster"):
            metrics = [
                    Prometheus("metrics01") >> Prometheus("alertmanger01"),
                    Prometheus("metrics02") >> Prometheus("alertmanger02"),
                    ]

        with Cluster("AWS services"):
            aws_group = [
                    EC2("service01") << Edge(style="dotted",
                                             color="red") << metrics,
                    EC2("service02") << Edge(style="dotted",
                                             color="red") << metrics,
                    ]

    loadbalancer >> metrics

    Ansible("ansible") >> metrics
    metrics >> Edge(style="dashed",
                    label="ec2 read permissions") >> General("AWS API")

    metrics >> Edge(style="dashed",
                         label="non-critical") >> Slack("rocky-alerts")
    metrics >> Edge(style="dashed",
                         label="critical") >> Pushover("tbd")
    ELB("metrics.rockylinux.org") >> Edge(label="TCP3000") >> dashboard
    with Cluster("Cloudvider"):
        cloudvider_group = [
                Server("server01") << Edge(style="dotted",
                                           color="red") << metrics,
                Server("server02") << Edge(style="dotted",
                                           color="red") << metrics,
                ]

    with Cluster("Spry Servers"):
        spry_group = [
                Server("server01") << Edge(style="dotted",
                                           color="red") << metrics,
                Server("server02") << Edge(style="dotted",
                                           color="red") << metrics,
                ]

    # metrics >> aws_group
    # metrics >> spry_group
    # metrics >> cloudvider_group
