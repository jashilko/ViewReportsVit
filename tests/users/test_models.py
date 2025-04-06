import pytest
from users.models import SiteUser  # Замените your_module на имя вашего модуля


@pytest.fixture
def sample_user():
    """Фикстура для создания тестового пользователя."""
    return SiteUser(
        id=1,
        phone_number="1234567890",
        password="secure_password",
        is_operator=True,
        is_teamlead=False,
        is_controller=False,
        is_admin=False,
        phone_teamleader="0987654321"
    )


def test_user_model_initialization(sample_user):
    """Тест инициализации пользователя."""
    assert sample_user.id == 1
    assert sample_user.phone_number == "1234567890"
    assert sample_user.password == "secure_password"
    assert sample_user.is_operator is True
    assert sample_user.is_teamlead is False
    assert sample_user.is_controller is False
    assert sample_user.is_admin is False
    assert sample_user.phone_teamleader == "0987654321"


def test_user_model_to_dict_method(sample_user):
    """Тест метода to_dict()."""
    user_dict = sample_user.to_dict()

    assert user_dict["id"] == 1
    assert user_dict["phone_number"] == "1234567890"
    assert user_dict["is_operator"] is True
    assert user_dict["is_teamlead"] is False
    assert user_dict["is_controller"] is False
    assert user_dict["is_admin"] is False
    assert user_dict["phone_teamleader"] == "0987654321"
    assert user_dict["role"] == "Оператор"


def test_user_model_admin_role():
    """Тест роли администратора."""
    admin_user = SiteUser(
        id=2,
        phone_number="admin_phone",
        password="admin_pass",
        is_operator=False,
        is_admin=True,
        phone_teamleader="some_leader"
    )
    user_dict = admin_user.to_dict()
    assert user_dict["role"] == "Админ"


def test_user_model_controller_role():
    """Тест роли контролера."""
    controller_user = SiteUser(
        id=3,
        phone_number="controller_phone",
        password="controller_pass",
        is_operator=False,
        is_controller=True,
        phone_teamleader="some_leader"
    )
    user_dict = controller_user.to_dict()
    assert user_dict["role"] == "Контролер"


def test_user_model_teamlead_role():
    """Тест роли руководителя группы."""
    teamlead_user = SiteUser(
        id=4,
        phone_number="teamlead_phone",
        password="teamlead_pass",
        is_operator=False,
        is_teamlead=True,
        phone_teamleader="some_leader"
    )
    user_dict = teamlead_user.to_dict()
    assert user_dict["role"] == "Руководитель группы"

def test_user_model_repr_method(sample_user):
    """Тест метода __repr__."""
    assert repr(sample_user) == "SiteUser(id=1)"