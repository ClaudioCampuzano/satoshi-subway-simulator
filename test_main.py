from main import subwayNetwork
import pytest

@pytest.mark.parametrize(
    "initialNode,finalNode, typeStation, expected",
    [
        ('A','F','','Shortest path = A->B->C->D->E->F'),
        ('A','F','red','Shortest path = A->B->C->H->F'),
        ('a','f','','Out-of-route stations, check network topology'),
        ('A','H','green','Out-of-route stations, check network topology'),
        ('A','H','blue','Wrong train color, available green and red'),
        ('A','A','','Station starts and ends the same')
    ]
    
)
def test_subwayNetwork(initialNode,finalNode, typeStation, expected):
    var = subwayNetwork('networkTopololy.json')
    assert var.findShortestPath(initialNode,finalNode, typeStation) == expected