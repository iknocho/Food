import pytest
from fastapi import Depends

def make_food_data():
    return {
        "food_code": "TST123",
        "group_name": "테스트군",
        "food_name": "테스트식품",
        "research_year": "2024",
        "maker_name": "테스트제조사",
        "ref_name": "테스트출처",
        "serving_size": 100.0,
        "calorie": 200.0,
        "carbohydrate": 30.0,
        "protein": 10.0,
        "province": 5.0,
        "sugars": 2.0,
        "salt": 1.0,
        "cholesterol": 0.5,
        "saturated_fatty_acids": 0.2,
        "trans_fat": 0.1
    }

@pytest.fixture(scope="module")
def food_id(client):
    # 생성
    response = client.post("/foods/", json=make_food_data())
    assert response.status_code == 201
    data = response.json()
    uid = data["uid"]
    yield uid
    # 삭제 (테스트 종료 후)
    client.delete(f"/foods/{uid}")


def test_create_food(client):
    response = client.post("/foods/", json=make_food_data())
    assert response.status_code == 201
    data = response.json()
    assert data["food_name"] == "테스트식품"
    # 생성 후 삭제
    client.delete(f"/foods/{data['uid']}")


def test_get_food_by_id(client, food_id):
    response = client.get(f"/foods/{food_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["uid"] == food_id
    assert data["food_name"] == "테스트식품"


def test_get_food_list(client):
    response = client.get("/foods/?food_name=테스트식품")
    assert response.status_code == 200
    data = response.json()
    print("데이터 :",data )
    assert "items" in data
    assert any(item["food_name"] == "테스트식품" for item in data["items"])


def test_update_food(client, food_id):
    update_data = {"food_name": "수정된식품"}
    response = client.patch(f"/foods/{food_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["food_name"] == "수정된식품"


def test_delete_food(client):
    # 먼저 생성
    response = client.post("/foods/", json=make_food_data())
    assert response.status_code == 201
    uid = response.json()["uid"]
    # 삭제
    del_response = client.delete(f"/foods/{uid}")
    assert del_response.status_code == 204
    # 삭제 후 조회 시 404여야 함
    get_response = client.get(f"/foods/{uid}")
    assert get_response.status_code == 404
