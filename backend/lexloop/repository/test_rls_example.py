"""Example tests showing RLS usage."""

from fastapi.testclient import TestClient


def test_with_admin_client(client: TestClient) -> None:
    """Default: uses admin client, sees all data (bypasses RLS)."""
    response = client.post(
        "/nodes", json={"term": "Test", "definition": "Admin's node"}
    )
    assert response.status_code == 201


def test_with_user_client(client_as_user1: TestClient) -> None:
    """Use test_user fixture - RLS is active."""
    # Create node as user1
    response = client_as_user1.post(
        "/nodes", json={"term": "User1 Node", "definition": "Belongs to user1"}
    )
    assert response.status_code == 201

    # User1 can see their own node
    nodes = client_as_user1.get("/nodes").json()
    assert len(nodes) == 1
    assert nodes[0]["term"] == "User1 Node"


def test_rls_isolation(
    client_as_user1: TestClient, client_as_user2: TestClient
) -> None:
    """Test that users can't see each other's data."""
    # User1 creates a node
    client_as_user1.post(
        "/nodes", json={"term": "User1 Node", "definition": "Private"}
    )

    # User2 creates a node
    client_as_user2.post(
        "/nodes", json={"term": "User2 Node", "definition": "Also private"}
    )

    # User1 only sees their own node
    user1_nodes = client_as_user1.get("/nodes").json()
    assert len(user1_nodes) == 1
    assert user1_nodes[0]["term"] == "User1 Node"

    # User2 only sees their own node
    user2_nodes = client_as_user2.get("/nodes").json()
    assert len(user2_nodes) == 1
    assert user2_nodes[0]["term"] == "User2 Node"
