import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import LogoVertical from "../assets/images/Logo-vertical.svg";
// CSS импорты
import "../assets/styles/font.css";
import "../assets/styles/buttons.css";
import "../assets/styles/colors.css";
import "../assets/styles/text.css";
import "../assets/styles/authPage.css";

const AuthPage = () => {
  const [realname, setRealname] = useState("");
  const [username, setUsername] = useState(""); // Для входа используем username
  const [password, setPassword] = useState("");
  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleusername = async () => {
    const formData = new URLSearchParams();
    formData.append("username", username); // Используем username для входа
    formData.append("password", password);

    try {
      const response = await fetch(`api/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(), // Правильный формат для x-www-form-urlencoded
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка входа");
      }

      const data = await response.json();
      localStorage.setItem("access_token", data.access_token);
      navigate("/home");
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

    // Валидация полей
    if (isRegistering) {
      // При регистрации проверяем realname и username
      if (!realname || !username || !password) {
        setError("Пожалуйста, заполните все поля");
        return;
      }
    } else {
      // При входе проверяем только username и password
      if (!username || !password) {
        setError("Пожалуйста, заполните все поля");
        return;
      }
    }

    try {
      if (isRegistering) {
        await handleRegister();
      } else {
        await handleUsername();
      }
    } catch (err) {
      setError(err.message || "Произошла ошибка. Попробуйте снова.");
      console.error("Auth error:", err);
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
                  required={isRegistering}
                />
              </div>
            )}

            {/* Поле username (используется для входа) */}
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
