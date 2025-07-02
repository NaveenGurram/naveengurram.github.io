from ast import Lambda
from types import LambdaType
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.storage import SimpleStorageServiceS3,S3
from diagrams.programming.framework import Angular, DotNet
from diagrams.onprem.database import Oracle
from diagrams.aws.database import DocumentDB
from diagrams.programming.framework import Spring
from diagrams.aws.security import Guardduty
from diagrams.aws.compute import Lambda
from diagrams.aws.compute import Fargate
from diagrams.aws.database import RDSOracleInstance
from diagrams.c4 import Person, Container, Database, System, SystemBoundary, Relationship
from diagrams.aws.mobile import APIGateway
from diagrams.onprem.monitoring import Splunk
from diagrams.programming.language import Csharp, Java

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
    "bgcolor": "#90EE90",
}
with Diagram(show=True, direction="BT"):
    with Cluster("Phase2 System Architecture",graph_attr=cluster_40_graph_attr):

        with Cluster("Classic",graph_attr=cluster_20_graph_attr):
            classic = DotNet("Classic")
            oracle =  RDSOracleInstance("Oracle")
            classic >> Edge(label="Reads/Writes") >> oracle

        with Cluster("Reference", graph_attr=cluster_20_graph_attr_green_bg):
            referenceApi = APIGateway("Reference Services API")
            referenceLambda = Lambda("Reference Services Lambda")

        with Cluster("Form Fillings", graph_attr=cluster_20_graph_attr_green_bg):
            finforms = Angular("Finforms")
            dcs = Fargate("DataCollection")
            dcsDocDb = DocumentDB("DCS")
            fistDocDb = DocumentDB("Fist")
            fist = Fargate("Fist")
            fistS3 = S3("fist")
            fistQueue = SQS("Fist-Queue")
            dcsTopic = SNS("DCS-Topic")
            guardDuty = Guardduty("GuardDuty")

            finforms >> dcs >> dcsDocDb
            finforms >>  fist >> fistDocDb
            finforms >> fistS3 >> fistQueue
            fistS3 >> guardDuty >> fistQueue
            fistQueue >> fist
            dcs >> dcsTopic
            dcs >> fist
            dcs >> referenceApi
            finforms >> referenceApi >> referenceLambda

        with Cluster("IAM", graph_attr=cluster_20_graph_attr):
            iamUi = Angular("Account Management UI")
            accountManagementApi = APIGateway("Account Management API")
            accountManagementLambda = Lambda("Account Management Lambda")
            socure = Container(name="Socure")
            iamAuthorizer = Container(name="Authorizer")
            idGateway = Container(name="Identity Gateway")

            iamUi >> accountManagementApi >> accountManagementLambda >> oracle
            accountManagementLambda >> socure


        with Cluster("Entity Profile", graph_attr=cluster_20_graph_attr_green_bg):
            entityProfileUi = Angular("EntityProfile")
            entityProfileApi = APIGateway("Entity Profile API")
            entityProfileLambda = Lambda("Entity Profile Lambda")

            entityProfileUi >> entityProfileApi >> entityProfileLambda >> Edge(label="Reads/Writes") >> oracle


        with Cluster("Data Services", graph_attr=cluster_20_graph_attr_green_bg):
            dataServicesApi = APIGateway("Data Services API")
            dataServicesLambda = Lambda("Data Services Lambda")
            dataServicesQueue = SQS("Data Services Queue")

            dataServicesApi >> dataServicesLambda >>  oracle
            dcs >> dataServicesApi
            fist >>  dataServicesApi
            dataServicesQueue >> dataServicesLambda
            dcsTopic >> dataServicesQueue

        with Cluster("Payments", graph_attr=cluster_20_graph_attr_green_bg):
            paymentApi = APIGateway("Payment Services API")
            paymentLambda = Lambda("Payment Services Lambda")

            paymentApi >> paymentLambda
            paymentLambda >> dataServicesApi
            paymentLambda >> entityProfileApi
            finforms >> paymentApi
