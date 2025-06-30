import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import LabelWithIcon from "./iconTextLabel";
import PaymentForm from "./paymentForm";
import Modal from "./modal";
import Star from "../../assets/images/Star.svg";
import "../../assets/styles/headers.css";
import "../../assets/styles/grid.css";
import "../../assets/styles/text.css";

const HomeworkCard = ({
  number,
  taskText,
  taskTextFull,
  price,
  //tag,
  rating = "N/A",
}) => {

  const [modalActive, setModalActive] = useState(false);
  console.log({ number, taskText, taskTextFull, price, rating });
  return (
    <div className="hwPanel">
      {price == 0 ? (
        <Modal active={modalActive} setActive={setModalActive}>
          <PreviewHomework
           gdzId={number}
            setActive={setModalActive}
          />
        </Modal>
      ) : (
        <Modal active={modalActive} setActive={setModalActive}>

        </Modal>
      )}
      <div className="category-left-box">
        <h1>Задача {number}</h1>
        <h2>{taskText}</h2>
        <h3>{taskTextFull}</h3>
        <LabelWithIcon icon={Star} className="ratingLabel">
          {rating}
        </LabelWithIcon>
        <button className="button" onClick={() => setModalActive(true)}>
          {price == 0 ? "Бесплатно" : price + " руб"}
        </button>
      </div>
    </div>
  );
};

export default HomeworkCard;
