import React, { useRef, useState } from "react";
import UploadIcon from "../../assets/images/UploadSimple.svg";
import "../../assets/styles/fileUpload.css";

const FileUploadButton = ({ onFileSelect }) => {
  const [fileName, setFileName] = useState("");
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    processFile(file);
    e.target.value = "";
  };

  const processFile = (file) => {
    if (!file) return;

    const validExtensions = ['.png', '.jpeg', '.jpg'];
    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(`.${fileExtension}`)) {
      alert("Допустимы только PNG, JPEG или JPG");
      return;
    }

    const MAX_SIZE = 5 * 1024 * 1024;
    if (file.size > MAX_SIZE) {
      alert("Файл слишком большой (макс. 5MB)");
      return;
    }

    setFileName(file.name);
    onFileSelect(file);
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="file-upload-container" onClick={triggerFileInput}>
      <input
        type="file"
        ref={fileInputRef}
        accept=".png,.jpeg,.jpg"
        onChange={handleFileChange}
        className="file-input"
        aria-label="Выберите файл для загрузки"
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