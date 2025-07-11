import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom2 from "../components/ui/buttomHeader2";
import HomeWorkPanel from "../components/ui/hwPanelMe";
import ProfileCard from "../components/ui/profileCard";
import "../assets/styles/grid.css";

const ProfilePage = () => {
    const [profileData, setProfileData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const pageSize = 10;
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfileData = async () => {
            try {
                const token = localStorage.getItem("access_token");
                if (!token) {
                    throw new Error("Требуется авторизация. Пожалуйста, войдите в систему.");
                }

                const response = await fetch('/api/profile/data', {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || "Ошибка при загрузке профиля");
                }

                const data = await response.json();
                setProfileData(data);
            } catch (err) {
                setError(err.message);
                console.error("Ошибка:", err);
                if (err.message.includes("Требуется авторизация") || err.message.includes("Неверные учетные данные")) {
                    localStorage.removeItem("access_token");
                    navigate("/", {replace: true });
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

    const totalPages = Math.ceil(profileData.gdz_list.length / pageSize);
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const paginatedGdzList = profileData.gdz_list.slice(startIndex, endIndex);

    const goToNextPage = () => {
        if (currentPage < totalPages) {
            setCurrentPage(currentPage + 1);
        }
    };

    const goToPrevPage = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    const goToPage = (page) => {
        if (page >= 1 && page <= totalPages) {
            setCurrentPage(page);
        }
    };

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

                {paginatedGdzList.length > 0 ? (
                    paginatedGdzList.map((gdz) => {
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
                    })
                ) : (
                    <p>ГДЗ пока нет</p>
                )}

                {profileData.gdz_list.length > pageSize && (
                    <div className="pagination">
                        <button
                            onClick={goToPrevPage}
                            disabled={currentPage === 1}
                            className="pagination-button"
                            aria-label="Предыдущая страница"
                        >
                            Назад
                        </button>
                        <div className="pagination-pages">
                            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                                <button
                                    key={page}
                                    onClick={() => goToPage(page)}
                                    className={`pagination-button pagination-page ${currentPage === page ? "active" : ""}`}
                                    aria-label={`Перейти на страницу ${page}`}
                                    aria-current={currentPage === page ? "page" : undefined}
                                >
                                    {page}
                                </button>
                            ))}
                        </div>
                        <button
                            onClick={goToNextPage}
                            disabled={currentPage === totalPages}
                            className="pagination-button"
                            aria-label="Следующая страница"
                        >
                            Вперед
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ProfilePage;