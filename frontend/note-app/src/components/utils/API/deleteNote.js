import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function deleteNoteAPI(id) {
  const url = `/note/note/${id}`
  const response = await refreshAPI(
    async () => await fetch(baseurl + url, {
      method: "delete",
      headers: {}
    })
  )
  return response
}