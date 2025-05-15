import LabelWithIcon from "./iconTextLabel";
import Star from "../../assets/images/Star.svg";
const ProfileCard = ({ username, rating = "N/A" }) => {
  return (
    <div className="hwPanel">
      <div className="category-left-box">
        <h1>username</h1>
        {/* <h2>login</h2> */}
        <h3>description</h3>
        <LabelWithIcon icon={Star} className="ratingLabel">
          {rating}
        </LabelWithIcon>
      </div>
      <button className="button">Мои ответы</button>
    </div>
  );
};

export default ProfileCard;
