import { useParams, useNavigate } from "react-router-dom";
import PreviewHomework from "../components/ui/previewHomework";
//import "../assets/styles/gdzPage.css";

const GdzPage = () => {
    const { gdzId } = useParams();
    const navigate = useNavigate();

    return (
        <div className="gdz-page">
            <div className="gdz-page-container">
                <PreviewHomework
                    gdzId={gdzId}
                    onClose={() => navigate(-1)}
                    flagToNotSetRating={0}
                    isStandalonePage={true}
                />
            </div>
        </div>
    );
};

export default GdzPage;
