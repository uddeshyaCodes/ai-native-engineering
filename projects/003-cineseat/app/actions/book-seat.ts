"use server";

import { revalidatePath } from "next/cache";
import { auth } from "@/auth";
import { prisma } from "@/lib/prisma";

export async function bookSeat(
  seatId: string,
): Promise<{ ok: boolean; message: string }> {
  // Trust boundary: Auth <-> Data (slide 14). The session is confirmed
  // BEFORE any booking query runs. Not after. Not in parallel.
  const session = await auth();
  const email = session?.user?.email;

  if (!email) {
    return { ok: false, message: "Sign in before booking a seat." };
  }

  const seat = await prisma.seat.findUnique({ where: { id: seatId } });

  if (!seat) {
    return { ok: false, message: "That seat no longer exists." };
  }

  if (seat.status !== "available") {
    return {
      ok: false,
      message: `Row ${seat.row}, seat ${seat.number} was taken a moment ago. Pick another one.`,
    };
  }

  await prisma.$transaction([
    prisma.seat.update({ where: { id: seat.id }, data: { status: "booked" } }),
    prisma.booking.create({
      data: { seatId: seat.id, showtimeId: seat.showtimeId, userEmail: email },
    }),
  ]);

  revalidatePath(`/showtimes/${seat.showtimeId}`);

  return {
    ok: true,
    message: `Booked row ${seat.row}, seat ${seat.number}. Enjoy the film.`,
  };
}
