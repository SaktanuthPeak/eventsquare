import { SvelteKitAuth } from "@auth/sveltekit"
import Google from "@auth/sveltekit/providers/google"
import LINE from "@auth/sveltekit/providers/line"

export const { handle, signIn } =  SvelteKitAuth({ 
  providers: [
    Google,LINE
  ],
})