import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import RatingInput from "./ratePanel";
import defaultPhoto from "../../assets/images/image 6110.png";
import "../../assets/styles/font.css";
import "../../assets/styles/buttons.css";
import "../../assets/styles/colors.css";
import "../../assets/styles/text.css";
import "../../assets/styles/authPage.css";
import "../../assets/styles/photo.css";
import { UserContext } from "../../contexts/UserContext";

const PreviewHomework = ({ gdzId, onClose, flagToNotSetRating = 0, isStandalonePage = false }) => {
    const [data, setData] = useState({
        taskText: "Загрузка...",
        answerText: "Загрузка...",
        photoUrl: defaultPhoto,
        isLoading: true,
        error: null,
        ownerId: null,
        isFree: false, // Только isFree вместо price
    });

    const [isLoading, setIsLoading] = useState(true);
    const [userRating, setUserRating] = useState(0);
    const [isRatingSubmitting, setIsRatingSubmitting] = useState(false);
    const navigate = useNavigate();
    const [error, setError] = useState(false);

    const { user } = useContext(UserContext);
    const currentUserId = user.id;

    const handleImageLoad = () => {
        setIsLoading(false);
    };

    const handleImageError = () => {
        setError(true);
        setIsLoading(false);
    };

    useEffect(() => {
        const fetchGdzData = async () => {
            try {
                const token = localStorage.getItem("access_token");
                const response = await fetch(`/api/gdz/${gdzId}/full`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error(response.status === 403
                        ? "Нет доступа к этому ГДЗ"
                        : "Ошибка загрузки");
                }

                const gdzData = await response.json();

                setData({
                    taskText: gdzData.full_description,
                    answerText: gdzData.content_text,
                    photoUrl: gdzData.content,
                    isLoading: false,
                    error: null,
                    ownerId: gdzData.owner_id,
                    isFree: gdzData.price === 0, // Определяем бесплатность
                });
            } catch (err) {
                setData({
                    taskText: "Ошибка загрузки",
                    answerText: "Ошибка загрузки",
                    photoUrl: defaultPhoto,
                    isLoading: false,
                    error: err.message,
                    isFree: true,
                });
            }
        };

        fetchGdzData();
    }, [gdzId]);

    const handleClose = () => {
        if (onClose) onClose();
        else navigate(-1);
    };

    const handleSubmitRating = async () => {
        if (userRating === 0) {
            handleClose();
            return;
        }

        setIsRatingSubmitting(true);
        try {
            const token = localStorage.getItem("access_token");
            const response = await fetch('/api/gdz/rate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    gdz_id: gdzId,
                    value: userRating
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Ошибка оценки');
            }

            handleClose();
        } catch (err) {
            setData(prev => ({ ...prev, error: err.message }));
        } finally {
            setIsRatingSubmitting(false);
        }
    };

    const isOwner = currentUserId && data.ownerId && currentUserId.toString() === data.ownerId.toString();
    if (data.isLoading) return <div className="loading">Загрузка ГДЗ...</div>;

    return (
        <div className="auth-form-container">
            <h2 className="bold">Задача</h2>
            <h4>{data.taskText}</h4>
            <h2 className="bold">Решение</h2>
            <div className="photo-container">
                {data.isLoading && <div className="photo-loader">Загрузка...</div>}
                {error ? (
                    <div className="photo-error">Ошибка загрузки</div>
                ) : (
                        <img
                            src={data.photoUrl}
                            className="photo-image"
                            onLoad={handleImageLoad}
                            onError={handleImageError}
                        />
                    )}
            </div>
            <h2 className="bold">Ответ</h2>
            <h4>{data.answerText}</h4>

            {/* Показываем звёзды только для платных ГДЗ, если пользователь не владелец */}
            {flagToNotSetRating === 0 && !isOwner && !data.isFree && (
                <>
                    <RatingInput
                        label="Оцените работу пользователя"
                        onRatingChange={setUserRating}
                        currentRating={userRating}
                    />
                    {data.error && <p className="error-text">{data.error}</p>}
                </>
            )}
            <div style={{
                display: "flex",
                justifyContent: "center",
                marginTop: "16px",
            }}>
                <div className="modal-actions">
                    <button
                        className="button"
                        onClick={handleSubmitRating}
                        disabled={isRatingSubmitting}
                    >
                        {isRatingSubmitting ? 'Сохранение...' : 'OK'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default PreviewHomework;