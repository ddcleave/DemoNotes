import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function addTagAPI(noteid, tag) {
  const url = '/note/tag/add'
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