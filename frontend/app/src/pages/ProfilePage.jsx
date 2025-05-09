import { Link } from "react-router-dom";

const ProfilePage = () => {
  return (
    <div>
      <h1>{"Home Page"}</h1>
      <p>In progress... Go away!</p>
      <Link to={"/"}>
        <button className="buttonGreen">Home</button>
      </Link>
    </div>
  );
};

export default ProfilePage;
