function LabelWithIcon({ icon, children, className }) {
  return (
    <label className={className}>
      <img src={icon} />
      <span>{children}</span>
    </label>
  );
}
export default LabelWithIcon;
