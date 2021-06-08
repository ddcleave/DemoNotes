import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function removeTagAPI(noteid, tag) {
  const url = '/note/tag/remove'
  const dataForRequest = {
    'note': noteid,
    'tag': tag
  }
  const response = await refreshAPI(
    async () => await fetch(baseurl + url, {
      method: "post",
      headers: {},
      body: JSON.stringify(dataForRequest)
    })
  )
  return response
}