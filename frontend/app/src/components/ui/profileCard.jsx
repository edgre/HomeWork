import LabelWithIcon from "./iconTextLabel";
import StarIcon from "../../assets/images/Star.svg";
import "../../assets/styles/headers.css";
import "../../assets/styles/grid.css";
import "../../assets/styles/text.css";

const ProfileCard = ({ username, realname, rating, isElite }) => {
    return (
        <div className="profileCard">
            <h1 className="bold">{realname}</h1>
            {username && <h3>{username}</h3>}
            <div className="profileStats">
                <div>
                    <h3>Рейтинг</h3>
                    <LabelWithIcon icon={StarIcon} className="ratingLabel">
                        {rating ? rating.toFixed(1) : "Нет оценок"}
                    </LabelWithIcon>
                </div>
                {isElite && (
                    <div>
                        <h3>Статус</h3>
                        <p>Премиум</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ProfileCard;
