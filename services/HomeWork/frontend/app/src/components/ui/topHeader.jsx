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
        localStorage.removeItem("access_token");
        setUser(null);

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
                <h3>{user?.realname || "Гость"}</h3>

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

                <button className="buttonWhite" onClick={handleLogout}>
                    Выйти
        </button>
            </nav>
        </header>
    );
};

export default HeaderTop;
