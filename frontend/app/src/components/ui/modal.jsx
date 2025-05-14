import React from "react";
import { Link } from "react-router-dom";
import "../../assets/styles/modal.css";
import "../../assets/styles/grid.css";
import "../../assets/styles/text.css";

const Modal = ({ active, setActive, children }) => {
  return (
    <div
      className={active ? "modal active" : "modal"}
      onClick={() => setActive(false)}
    >
      <div
        className={active ? "modal-container active" : "modal-container"}
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>
  );
};

export default Modal;
