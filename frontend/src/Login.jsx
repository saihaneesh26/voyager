import { GoogleLogin } from '@react-oauth/google'

function Login() {

  const handleSuccess = (credentialResponse) => {
    console.log(credentialResponse)
  }

  const handleError = () => {
    console.log('Login Failed')
  }

  return (
    <div>
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={handleError}
      />
    </div>
  )
}

export default Login