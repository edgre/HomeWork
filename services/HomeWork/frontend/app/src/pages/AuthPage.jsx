import React, { useState, useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import LogoVertical from "../assets/images/Logo-vertical.svg";
import "../assets/styles/font.css";
import "../assets/styles/buttons.css";
import "../assets/styles/colors.css";
import "../assets/styles/text.css";
import "../assets/styles/authPage.css";
import { UserContext } from "../contexts/UserContext";

const AuthPage = () => {
  const [realname, setRealname] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const { setUser } = useContext(UserContext);

  const handleLogin = async () => {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
      const response = await fetch(`api/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка входа");
      }

      const data = await response.json();
      localStorage.setItem("access_token", data.access_token);

      const userResponse = await fetch("/api/users/me", {
        headers: {
          Authorization: `Bearer ${data.access_token}`,
        },
      });

      if (!userResponse.ok) {
        throw new Error("Не удалось загрузить данные пользователя");
      }

      const userData = await userResponse.json();

      setUser({
        id: userData.id,
        username: userData.username,
        realname: userData.realname,
        rating: parseFloat(userData.rating),
        access_token: data.access_token,
        has_draft: userData.has_draft,
      });

      const isStateValid =
        location.state?.timestamp &&
        Date.now() - location.state.timestamp < 60000;

      const from = isStateValid && userData.id ? location.state.from : "/home";

      navigate(from, { replace: true, state: null });
    } catch (err) {
      throw err;
    }
  };

  const handleRegister = async () => {
    try {
      const response = await fetch(`api/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
          realname: realname,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка регистрации");
      }

      setError("Регистрация успешна! Теперь вы можете войти.");
      setIsRegistering(false);
      setRealname("");
      setUsername("");
      setPassword("");
    } catch (err) {
      throw err;
    }
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setError("");

    try {
    if (isRegistering) {
      if (!realname || !username || !password) {
        setError("Пожалуйста, заполните все поля");
        return;
      }
      await handleRegister();
    } else {
      if (!username || !password) {
        setError("Пожалуйста, заполните все поля");
        return;
      }
      await handleLogin();
    }
  } catch (err) {
    setError(err.message);
  }
};

  return (
    <div className="container">
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <div style={{ margin: "32px" }}>
          <img
            src={LogoVertical}
            width="400"
            height="170"
            alt="Домашка Плюс"
            loading="lazy"
          />
        </div>

        <div className="auth-form-container">
          <h1
            className="h1"
            style={{ verticalAlign: "center", justifyContent: "center" }}
          >
            Добрый день
          </h1>
          <h2
            style={{
              marginTop: "5px",
              verticalAlign: "center",
              justifyContent: "center",
            }}
          >
            Пожалуйста авторизуйтесь
          </h2>

          <form className="auth-form" onSubmit={handleAuth}>
            <div className="form-group" style={{ padding: "0px" }}>
              <label className="switch">
                <input
                  type="checkbox"
                  checked={isRegistering}
                  onChange={() => setIsRegistering(!isRegistering)}
                />
                <span className="slider">
                  <span className="text-off">Вход</span>
                  <span className="text-on">Регистрация</span>
                </span>
              </label>
            </div>
            {isRegistering && (
              <div className="form-group">
                <input
                  type="text"
                  id="realname"
                  className="inputBox"
                  placeholder="Никнейм"
                  value={realname}
                  onChange={(e) => setRealname(e.target.value)}
                  required
                />
              </div>
            )}

            <div className="form-group">
              <input
                type="text"
                id="username"
                className="inputBox"
                placeholder="Логин"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <input
                type="password"
                id="password"
                className="inputBox"
                placeholder="Пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <button
                type="submit"
                className="button"
                style={{ marginTop: "8px" }}
              >
                {isRegistering ? "Зарегистрироваться" : "Войти"}
              </button>
            </div>
          </form>
        </div>
      </div>
      {error && (
        <div className="auth-error-container">
          <div className="h5-error">{error}</div>
        </div>
      )}
    </div>
  );
};

export default AuthPage;
