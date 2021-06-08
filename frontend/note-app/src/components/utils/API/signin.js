import { baseurl } from "./baseurl"

export default async function signinAPI(username, password, fingerprint) {
  let url = '/api/v1/token'
  let data = new FormData()
  data.append("username", username)
  data.append("password", password)
  data.append("fingerprint", fingerprint)

  const response = await fetch(baseurl + url, {
    method: "post",
    headers: {},
    body: data
  })
  return response
}