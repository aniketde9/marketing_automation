import { redirect } from "next/navigation";

export default function SetupApiKeyRedirect() {
  // Redirect old route to new dashboard route
  redirect("/api-key");
}
