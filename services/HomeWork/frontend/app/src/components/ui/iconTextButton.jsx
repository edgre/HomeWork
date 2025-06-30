function ButtonWithIcon({ icon, children, onClick, className }) {
  return (
    <button onClick={onClick} className={className}>
      <img src={icon} />
      <span style={{ textDecoration: "none" }}>{children}</span>
    </button>
  );
}
export default ButtonWithIcon;
