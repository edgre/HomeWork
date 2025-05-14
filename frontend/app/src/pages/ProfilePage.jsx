import { Link } from "react-router-dom";
import HeaderTop from "../components/ui/topHeader";
import HeaderButtom2 from "../components/ui/buttomHeader2";
import HomeWorkPanel from "../components/ui/hwPanelMe";
import ProfileCard from "../components/ui/profileCard";
import "../assets/styles/grid.css";

const ProfilePage = () => {
  return (
    <div>
      <HeaderTop username={"Gleb"} />
      <HeaderButtom2 />

      <div className="grid">
        <ProfileCard username={"Gleb"} />
        <HomeWorkPanel
          subject={"Алгебра"}
          taskText={"Решить систему уравнений"}
        />
      </div>
    </div>
  );
};

export default ProfilePage;
