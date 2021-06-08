import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function getNotesAPI(position, tag) {
  const url = new URL(baseurl + '/note/notes')
  const params = new URLSearchParams()
  if (position !== null) {
    params.append("position", position)
  }
  if (tag !== '') {
    params.append("tag", tag)
  }
  url.search = params

  const response = await refreshAPI(async () => await fetch(url))
  return response
}