import React, { useState } from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { LoadingOutlined } from '@ant-design/icons';
import './LoginPage.css';
import { BACKEND_URL } from '../config';

const LoginPage = ({ onLogin }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGoogleSuccess = async (credentialResponse) => {
    setError('');
    setLoading(true);

    try {
      // Send Google token to backend
      const response = await fetch(`${BACKEND_URL}/api/auth/google`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: credentialResponse.credential
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Store JWT token and user info
        localStorage.setItem('jwt_token', data.token);
        localStorage.setItem('user_info', JSON.stringify(data.user));
        
        // Call the onLogin callback
        onLogin(data.user);
      } else {
        setError(data.error || 'Login failed. Please try again.');
        setLoading(false);
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Network error. Please try again.');
      setLoading(false);
    }
  };

  const handleGoogleError = () => {
    setError('Google login failed. Please try again.');
    setLoading(false);
  };

  return (
    <section className="login-section">
      <div className="login">
        <div className="kosh-full-logo">
          <img
            src="/images/Kosh_Full_Logo.png"
            alt="logo"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
        <h2>Log in to your Account</h2>
        
        <div className="flex-column" style={{ marginTop: '2rem' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
              <LoadingOutlined style={{ fontSize: '2rem' }} />
              <p style={{ marginTop: '1rem' }}>Logging in...</p>
            </div>
          ) : (
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={handleGoogleError}
                useOneTap
                theme="outline"
                size="large"
                text="signin_with"
                shape="rectangular"
              />
            </div>
          )}

          {error && (
            <div className="error-message" style={{ textAlign: 'center', color: 'red', marginTop: '1rem' }}>
              {error}
            </div>
          )}
        </div>
      </div>
      
      <div className="flex items-center">
        <a
          className="term"
          href="https://www.kosh.ai/terms-of-use"
          target="_blank"
          rel="noreferrer"
        >
          Terms and Conditions
        </a>
        <span className="seperator" />
        <a
          className="term"
          href="https://www.kosh.ai/privacy-policy"
          target="_blank"
          rel="noreferrer"
        >
          Privacy Policy
        </a>
      </div>
    </section>
  );
};

export default LoginPage;