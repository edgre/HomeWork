import React, { useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { UserContext } from "../../contexts/UserContext";
import LogoHorizontal from "../../assets/images/Logo-horizontal.svg";
import LogoProfile from "../../assets/images/User.svg";
import "../../assets/styles/headers.css";

const HeaderTop = () => {
    const { user, setUser } = useContext(UserContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        // Очистка токена и пользователя
        localStorage.removeItem("access_token");
        setUser(null);

        // Переход на главную с заменой истории (чтобы сбросить location.state)
        navigate("/", { replace: true });
    };

    return (
        <header className="headerTop">
            <div>
                <Link to="/home">
                    <img
                        className="icon-button"
                        src={LogoHorizontal}
                        width="298"
                        height="48"
                        alt="Домашка Плюс"
                        loading="lazy"
                    />
                </Link>
            </div>
            <nav className="header-menu">
                {/* Отображаем имя пользователя или "Гость" */}
                <h3>{user?.realname || "Гость"}</h3>

                {/* Кнопка на профиль только если авторизован */}
                {user && (
                    <Link to="/me">
                        <img
                            className="icon-button"
                            src={LogoProfile}
                            width="32"
                            alt="Мой профиль"
                            loading="lazy"
                        />
                    </Link>
                )}

                {/* Кнопка выхода */}
                <button className="buttonWhite" onClick={handleLogout}>
                    Выйти
        </button>
            </nav>
        </header>
    );
};

export default HeaderTop;
