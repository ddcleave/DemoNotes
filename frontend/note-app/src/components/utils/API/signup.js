import { baseurl } from "./baseurl"

export default async function signupAPI(values) {
  const url = '/api/v1/signup'
  let data = new FormData()
  data.append("username", values.username)
  data.append("password", values.password)
  data.append("email", values.email)
  data.append("full_name", values.fullname)

  const response = await fetch(baseurl + url, {
    method: "post",
    headers: {},
    body: data
  })
  return response
}