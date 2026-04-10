function LoginPanel({ username, password, onUsernameChange, onPasswordChange, onLogin, onLogout, isLoggedIn }) {
  return (
    <form className="login" onSubmit={onLogin}>
      <h2>Auth</h2>
      <input value={username} onChange={(e) => onUsernameChange(e.target.value)} placeholder="username" />
      <input
        value={password}
        onChange={(e) => onPasswordChange(e.target.value)}
        type="password"
        placeholder="password"
      />
      <div className="row">
        <button type="submit">Login</button>
        <button type="button" className="secondary" onClick={onLogout}>
          Logout
        </button>
      </div>
      <small>{isLoggedIn ? 'Authenticated' : 'Guest mode'}</small>
    </form>
  )
}

export default LoginPanel
