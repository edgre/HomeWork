import "../../assets/styles/font.css";
import "../../assets/styles/buttons.css";
import "../../assets/styles/colors.css";
import "../../assets/styles/text.css";
import "../../assets/styles/authPage.css";

const PaymentForm = ({ nonce }) => {
  return (
    <div className="auth-form-container">
      <h1
        className="h1"
        style={{ verticalAlign: "center", justifyContent: "center" }}
      >
        Оплата
      </h1>
      <h2
        style={{
          marginTop: "5px",
          marginBottom: "16px",
          verticalAlign: "center",
          justifyContent: "center",
        }}
      >
        Введите данные вашей карты
      </h2>

      <h2
        style={{
          marginBottom: "16px",
        }}
      >
        Сеанс: {nonce}
      </h2>

      <form className="auth-form">
        <div className="form-group">
          <input
            type="text"
            id="username"
            className="inputBox"
            placeholder="Номер карты"
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <input
            type="text"
            id="password"
            className="inputBox"
            placeholder="CVV-код"
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <button type="submit" className="button" style={{ marginTop: "8px" }}>
            Оплатить
          </button>
        </div>
      </form>
    </div>
  );
};

export default PaymentForm;
