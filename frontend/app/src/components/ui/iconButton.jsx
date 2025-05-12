function IconButton({ icon, onClick, label }) {
  return (
    <button onClick={onClick} aria-label={label} className="icon-button">
      {icon}
    </button>
  );
}
