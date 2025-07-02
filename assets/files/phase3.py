from ast import Lambda
from types import LambdaType
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.integration import SNS, SQS
from diagrams.programming.framework import Angular, DotNet
from diagrams.onprem.database import Oracle
from diagrams.aws.database import DocumentDB
from diagrams.programming.framework import Spring
from diagrams.aws.compute import Lambda
from diagrams.aws.compute import Fargate
from diagrams.aws.database import RDSOracleInstance
from diagrams.c4 import Person, Container, Database, System, SystemBoundary, Relationship

cluster_40_graph_attr = {
    "labeljust": "100",
    "fontsize": "40",
    "fontname":"times-bold"
}

cluster_20_graph_attr = {
    "labeljust": "100",
    "fontsize": "20",
    "fontname":"times-bold"
}

cluster_20_graph_attr_green_bg = {
    "labeljust": "100",
    "fontsize": "20",
    "fontname":"times-bold",
    "bgcolor": "#90EE90"
}

with Diagram(show=True):
    with Cluster("Regulator Task Management Highlevel System Architecture",graph_attr=cluster_40_graph_attr):
        with Cluster("Classic",graph_attr=cluster_20_graph_attr):
            classic = DotNet("Classic")
            oracle =  RDSOracleInstance("Oracle")
            classicTopic = SNS("Classic-Topic")
            oracle >> Edge(label="Writes To") >> classic
            classic >> Edge(label="Reads From") >> oracle
            classic >> Edge(label="Generates Events") >> classicTopic

        with Cluster("Phase2 (FinForms + DECAF)", graph_attr=cluster_20_graph_attr):
            finforms = Angular("Finforms")
            decaf = Fargate("Decaf")
            decafTopic = SNS("Decaf-Topic")
            modQueue = SQS("Mod-Queue")
            mod = Lambda("Mod")

            finforms >> Edge(label="calls") >> decaf >> Edge(label="Generates Events") >> decafTopic >> Edge(label="Reads From") >> modQueue >> Edge(label="Process Events") >> mod >> Edge(label="Writes To") >> oracle

        with Cluster("Phase2 ", graph_attr=cluster_20_graph_attr):
            phase2Ui = Angular("UI")
            phase2Mod = Lambda("Mod")

            phase2Ui >> Edge(label="calls") >> phase2Mod >> Edge(label="writes to") >> oracle

        with Cluster("Other Classic Fillings", graph_attr=cluster_20_graph_attr):
            webapp = DotNet(".Net")
            webapp >> Edge(label="Writes To") >> oracle

        with Cluster("Phase3 Mod", graph_attr=cluster_20_graph_attr_green_bg):
            phase3Mod = Lambda("Phase3 Mod")
            phase3ModQueue = SQS("Phase3-Mod-Queue")

        with Cluster("RTM", graph_attr=cluster_20_graph_attr_green_bg):
            rtmUi = Angular("UI")
            rtmQueue = SQS("RTM-Queue")
            rtmTopic = SNS("RTM-Topic")
            docdb = DocumentDB("DataStore")
            wm = Lambda("WorkManagement")
            rtm = Lambda("RTM")
            classicTopic >> Edge(label="Reads From") >> rtmQueue >> Edge(label="Process Events") >> rtm
            rtmUi >> Edge(label="Interacts With") >> rtm
            rtm >> Edge(label="Creates Workitems") >> wm
            rtm >> Edge(label="Writes To") >> docdb
            rtm >> Edge(label="Generates Events") >>rtmTopic
            rtmTopic >> Edge(label="Pulls From") >> phase3ModQueue >> Edge(label="Process Events") >> phase3Mod
            phase3Mod >> Edge(label="Writes To") >> oracle
