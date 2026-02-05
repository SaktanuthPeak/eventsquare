import { getEvents, } from '$lib/client';
import type { PageServerLoad } from './$types';

export const load = (async ({params , locals}) => {

    const res = await getEvents({
        path:{
            event_id:params.event
        }
    });
    
    // const eventsWithImages = [];
        // for (const event of events) {
        //     if (event?.image?.file_id) {
        //         try {
        //             eventsWithImages.push({
        //                 ...event,
        //                 image_url: `${env.API_URL}/v1/events/image/${event?.image?.file_id}`
        //             });
        //         } catch (error) {
        //             console.log(error);
        //         }
        //     } else {
        //         eventsWithImages.push({
        //             ...event,
        //             image_url: null
        //         });
        //     }
        // }

        // return { events: eventsWithImages.filter((event) => event.event_status === 'active') };

    const user = locals.user;
 
    return {eventId: params.event,eventData:res.data,userData:user,image: res.data?.image_url,orgData:res.data?.organizer};
}) satisfies PageServerLoad;

