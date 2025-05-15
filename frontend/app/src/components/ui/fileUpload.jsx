import React, { useRef, useState } from "react";
import UploadIcon from "../../assets/images/UploadSimple.svg";
import "../../assets/styles/fileUpload.css";
import ButtonWithIcon from "./iconTextButton";

const FileUploadButton = () => {
  const [fileName, setFileName] = useState("");
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    processFile(file);
  };

  const processFile = (file) => {
    if (!file) return;

    const validTypes = [
      "image/png",
      "image/jpeg",
      "image/jpg",
      "application/pdf",
    ];

    if (!validTypes.includes(file.type)) {
      alert("Пожалуйста, выберите файл формата PNG, JPEG, JPG или PDF");
      return;
    }

    setFileName(file.name);
    console.log("Выбран файл:", file.name);
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="file-upload-container" onClick={triggerFileInput}>
      <input
        type="file"
        ref={fileInputRef}
        accept=".png,.jpeg,.jpg,.pdf"
        onChange={handleFileChange}
        className="file-input"
      />

      <div className="upload-content">
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <img src={UploadIcon} alt="Upload" className="upload-icon" />
          <h4 style={{ color: "#000" }}>{"Загрузить"}</h4>
        </div>

        {fileName && <p className="file-name">{fileName}</p>}
      </div>
    </div>
  );
};

export default FileUploadButton;
