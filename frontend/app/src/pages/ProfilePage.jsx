import React, { useState, useEffect } from "react";
import {useNavigate, Link} from "react-router-dom";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom2 from "../components/ui/buttomHeader2";
import HomeWorkPanel from "../components/ui/hwPanelMe";
import ProfileCard from "../components/ui/profileCard";
import "../assets/styles/grid.css";


const ProfilePage = () => {
    const [profileData, setProfileData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfileData = async () => {
            try {
                // 1. Получаем токен из localStorage
                const token = localStorage.getItem("access_token");

                // 2. Проверяем наличие токена
                if (!token) {
                    throw new Error("Требуется авторизация. Пожалуйста, войдите в систему.");
                }

                // 3. Делаем запрос с токеном
                const response = await fetch('/api/profile/data', {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                });

                // 4. Обрабатываем ответ
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || "Ошибка при загрузке профиля");
                }

                const data = await response.json();
                setProfileData(data);
            } catch (err) {
                setError(err.message);

                // 5. Перенаправляем на страницу входа при ошибках авторизации
                if (err.message.includes("Требуется авторизация") || err.message.includes("Неверные учетные данные")) {
                    localStorage.removeItem("token");
                    navigate("/", { replace: true });
                }
            } finally {
                setLoading(false);
            }
        };

        fetchProfileData();
    }, [navigate]);

    if (loading) return <div className="loading">Загрузка профиля...</div>;
    if (error) return <div className="error">Ошибка: {error}</div>;
    if (!profileData) return <div>Данные профиля не найдены</div>;

    return (
        <div>
            <HeaderTop username={profileData.username} />
            <HeaderButtom2 />

            <div className="grid">
                <ProfileCard
                    username={profileData.username}
                    realname={profileData.realname}
                    rating={profileData.user_rating}
                    isElite={profileData.is_elite}
                />



                {profileData.gdz_list.map((gdz) => {
                    const subject = gdz.category?.split('_').pop() || "Без предмета";
                    return (

                        <HomeWorkPanel
                            key={gdz.id}
                            subject={subject}
                            taskText={gdz.description}
                            isOwner={gdz.is_owner}
                            price={gdz.price}
                            isElite={gdz.is_elite}
                            gdzId={gdz.id}
                        />
                    );
                })}
            </div>
        </div>
    );
};

export default ProfilePage;
