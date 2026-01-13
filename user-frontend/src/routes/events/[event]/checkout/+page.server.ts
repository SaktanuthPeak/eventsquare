import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { checkoutSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { fail, superValidate } from 'sveltekit-superforms';
import { createOrder, uploadSlip } from '$lib/client';


export const load = (async (params) => {
    const form = await superValidate(zod(checkoutSchema))
    // const eventRes = await getEventByIdWithAllData({
    //     path: {
    //         event_id: params.params.event
    //     }
    // });

    return {form,
        // eventData: eventRes.data
    };
}) satisfies PageServerLoad;

// export const actions = {
//     default: async (event) => {
//         const form = await superValidate(event, zod(checkoutSchema));
//         const accessToken = event.cookies.get('access_token');
 
//         const eventRes = await getEventByIdWithAllData({
//             path: {
//                 event_id: event.params.event
//             }
//         });

//         try {
//             const res = await createOrder({
//                 body: {
//                     owner_name: form.data.owner_name,
//                     co_owner_name: form.data.co_owner_name,
//                     owner_email: form.data.owner_email ,
//                     co_owner_phone: form.data.owner_phone,
//                     co_owner_email: form.data.co_owner_email,
//                     user_id: event.locals.user.id,
//                     ticket_type_id: ticketId || "",
//                     organizer_id : form.data.organizer_id,
//                     event_id: form.data.event_id,
//                     audience_per_ticket: form.data.audience_per_ticket,         
//                     total_amount: form.data.total_amount,
//                 }
//             })
       
//             if (!res.response.ok || !res.data?._id){
//                return fail(400, {
//                     form,
//                     type: 'error',
//                 });
//             }
            
//             // todo res.data._id != order.id this then when upload image it error
//             const resUploadIamge = await uploadSlip({
//                 headers: {
//                     Authorization: `Bearer ${accessToken}`
//                 },
//                 path: {
//                     order_id: res.data._id
//                 },
//                 body: {
//                     file: form.data.slip_id
//                 }
//             })

          
            
//         }catch (error) {
//             console.log(error);
//             return fail(500, {
//                 form,
//                 error: 'An error occurred while processing your request. Please try again later.'}
//             );
//         }
//     }
// }

