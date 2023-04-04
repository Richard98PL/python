from graphQLAPI import graphQLScenario
from restAPI import restAPIScenario
from soapAPI import soapAPIScenario
from cleanResults import cleanResults
cleanResults()


for i in range(10):
    SIZES = [100, 1000, 10000]

    for SIZE in SIZES:

        graphql_query = """
        query table($cursor: String) {
            uiapi {
            query {
                table(first: 200, after: $cursor, orderBy: {Name: {order: ASC}}) {
                edges {
                    node {
                    Id
                    Boolean__c {
                        value
                    }
                    Currency__c {
                        value
                    }
                    Date__c {
                        value
                    }
                    Date_Time__c {
                        value
                    }
                    Index__c {
                        value
                    }
                    Multi_Pick_List__c {
                        value
                    }
                    Number__c {
                        value
                    }
                    Picklist__c {
                        value
                    }
                    }
                }
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                }
            }
            }
        }
        """

        graphQLScenario(SCENARIO=1, DATA_SIZE=SIZE, graphql_query = graphql_query)
        restAPIScenario(SCENARIO=1, DATA_SIZE=SIZE, query = "SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X ORDER By Name ASC")
        soapAPIScenario(SCENARIO=1, DATA_SIZE=SIZE, query_string='SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X ORDER By Name ASC')





















        graphql_query = """
        query table($cursor: String) {
            uiapi {
            query {
                table(first: 200, after: $cursor, orderBy: {Name: {order: ASC}}) {
                edges {
                    node {
                    Id
                    }
                }
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                }
            }
            }
        }
        """

        graphQLScenario(SCENARIO=2, DATA_SIZE=SIZE, graphql_query = graphql_query)
        restAPIScenario(SCENARIO=2, DATA_SIZE=SIZE, query = "SELECT Id FROM X ORDER By Name ASC")
        soapAPIScenario(SCENARIO=2, DATA_SIZE=SIZE, query_string='SELECT Id FROM X ORDER By Name ASC')























        graphql_query = """
        query table($cursor: String) {
            uiapi {
            query {
                table(first: 200, after: $cursor, orderBy: {Name: {order: ASC}}, where: {Currency__c: {eq: 0.2022}} ) {
                edges {
                    node {
                    Id
                    }
                }
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                }
            }
            }
        }
        """

        graphQLScenario(SCENARIO=3, DATA_SIZE=SIZE, graphql_query = graphql_query)
        restAPIScenario(SCENARIO=3, DATA_SIZE=SIZE, query = "SELECT Id FROM X WHERE Currency__c = 0.2022 ORDER By Name ASC")
        soapAPIScenario(SCENARIO=3, DATA_SIZE=SIZE, query_string='SELECT Id FROM X WHERE Currency__c = 0.2022 ORDER By Name ASC')



















        graphql_query = """
        query table($cursor: String) {
            uiapi {
            query {
                table(first: 200, after: $cursor, orderBy: {Name: {order: ASC}}, where: {Index__c: {eq: "1"}} ) {
                edges {
                    node {
                    Id
                    }
                }
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                }
            }
            }
        }
        """

        graphQLScenario(SCENARIO=4, DATA_SIZE=SIZE, graphql_query = graphql_query)
        restAPIScenario(SCENARIO=4, DATA_SIZE=SIZE, query = "SELECT Id FROM X WHERE Index__c = '1' ORDER By Name ASC")
        soapAPIScenario(SCENARIO=4, DATA_SIZE=SIZE, query_string="SELECT Id FROM X WHERE Index__c = '1' ORDER By Name ASC")
























        graphql_query = """
        query table($cursor: String) {
            uiapi {
            query {
                table(first: 200, after: $cursor, orderBy: {Currency__c: {order: ASC}}) {
                edges {
                    node {
                    Id
                    Boolean__c {
                        value
                    }
                    Currency__c {
                        value
                    }
                    Date__c {
                        value
                    }
                    Date_Time__c {
                        value
                    }
                    Index__c {
                        value
                    }
                    Multi_Pick_List__c {
                        value
                    }
                    Number__c {
                        value
                    }
                    Picklist__c {
                        value
                    }
                    }
                }
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                }
            }
            }
        }
        """

        graphQLScenario(SCENARIO=5, DATA_SIZE=SIZE, graphql_query = graphql_query)
        restAPIScenario(SCENARIO=5, DATA_SIZE=SIZE, query = "SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X ORDER By Currency__c ASC")
        soapAPIScenario(SCENARIO=5, DATA_SIZE=SIZE, query_string='SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X ORDER By Currency__c ASC')

























        graphql_query = """
        query table($cursor: String) {
            uiapi {
            query {
                table(first: 200, after: $cursor, orderBy: {Index__c: {order: ASC}}) {
                edges {
                    node {
                    Id
                    Boolean__c {
                        value
                    }
                    Currency__c {
                        value
                    }
                    Date__c {
                        value
                    }
                    Date_Time__c {
                        value
                    }
                    Index__c {
                        value
                    }
                    Multi_Pick_List__c {
                        value
                    }
                    Number__c {
                        value
                    }
                    Picklist__c {
                        value
                    }
                    }
                }
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                }
            }
            }
        }
        """

        graphQLScenario(SCENARIO=6, DATA_SIZE=SIZE, graphql_query = graphql_query)
        restAPIScenario(SCENARIO=6, DATA_SIZE=SIZE, query = "SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X ORDER By Index__c ASC")
        soapAPIScenario(SCENARIO=6, DATA_SIZE=SIZE, query_string='SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X ORDER By Index__c ASC')





















        graphql_query = """
        query table($cursor: String) {
            uiapi {
            query {
                table(first: 200, after: $cursor, orderBy: {Name: {order: ASC}}, where: {Currency__c: {gt: 10}}) {
                edges {
                    node {
                    Id
                    Boolean__c {
                        value
                    }
                    Currency__c {
                        value
                    }
                    Date__c {
                        value
                    }
                    Date_Time__c {
                        value
                    }
                    Index__c {
                        value
                    }
                    Multi_Pick_List__c {
                        value
                    }
                    Number__c {
                        value
                    }
                    Picklist__c {
                        value
                    }
                    }
                }
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                }
            }
            }
        }
        """

        graphQLScenario(SCENARIO=7, DATA_SIZE=SIZE, graphql_query = graphql_query)
        restAPIScenario(SCENARIO=7, DATA_SIZE=SIZE, query = "SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X WHERE Currency__c > 10 ORDER By Name ASC")
        soapAPIScenario(SCENARIO=7, DATA_SIZE=SIZE, query_string='SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X WHERE Currency__c > 10 ORDER By Name ASC')





























        graphql_query = """
        query table($cursor: String) {
            uiapi {
            query {
                table(first: 200, after: $cursor, orderBy: {Name: {order: ASC}}, where: {Id: {inq: {Relationship_Table__c:{and:[{Id: {ne: null}}]}, ApiName: "table"} } }) {
                edges {
                    node {
                    Id
                    Boolean__c {
                        value
                    }
                    Currency__c {
                        value
                    }
                    Date__c {
                        value
                    }
                    Date_Time__c {
                        value
                    }
                    Index__c {
                        value
                    }
                    Multi_Pick_List__c {
                        value
                    }
                    Number__c {
                        value
                    }
                    Picklist__c {
                        value
                    }
                    }
                }
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                }
            }
            }
        }
        """

        graphQLScenario(SCENARIO=8, DATA_SIZE=SIZE, graphql_query = graphql_query)
        restAPIScenario(SCENARIO=8, DATA_SIZE=SIZE, query = "SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X WHERE Id IN (Select X FROM Relationship_Table__c) ORDER By Name ASC")
        soapAPIScenario(SCENARIO=8, DATA_SIZE=SIZE, query_string='SELECT Id, Boolean__c, Currency__c, Date__c, Date_Time__c, Index__c, Multi_Pick_List__c, Number__c, Picklist__c FROM X WHERE Id IN (Select X FROM Relationship_Table__c) ORDER By Name ASC')