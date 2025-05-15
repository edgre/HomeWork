import "../../assets/styles/font.css";
import "../../assets/styles/buttons.css";
import "../../assets/styles/colors.css";
import "../../assets/styles/text.css";
import "../../assets/styles/authPage.css";

import FileUploadButton from "./fileUpload";
import DropdownList from "./dropdownList";

const HomeworkCreate = () => {
  return (
    <div className="auth-form-container" style={{ marginTop: "42px" }}>
      <h1
        className="h1"
        style={{ verticalAlign: "center", justifyContent: "center" }}
      >
        Созданией своего гдз
      </h1>

      <form className="auth-form">
        <DropdownList />

        <div className="form-group">
          <h4 style={{ color: "#000", marginBottom: "8px" }}>
            Краткое описание задания
          </h4>
          <input
            type="text"
            // id="username"
            className="inputBox"
            placeholder=""
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <h4 style={{ color: "#000", marginBottom: "8px" }}>
            Полная формулировка задания
          </h4>
          <input
            type="text"
            // id="username"
            className="inputBox"
            placeholder=""
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <h4 style={{ color: "#000" }}>Цена</h4>
          <h4 style={{ marginBottom: "8px" }}>(Числом, 0 = бесплатно)</h4>

          <input
            type="text"
            className="inputBox"
            placeholder=""
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <h4 style={{ color: "#000", marginBottom: "8px" }}>Короткий ответ</h4>
          <input
            type="text"
            className="inputBox"
            placeholder=""
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <h4 style={{ color: "#000", marginBottom: "8px" }}>
            Загрузить решение
          </h4>
          <FileUploadButton />
        </div>
        <div className="form-group">
          <button type="submit" className="button" style={{ marginTop: "8px" }}>
            Опубликовать
          </button>
        </div>
      </form>
    </div>
  );
};

export default HomeworkCreate;
