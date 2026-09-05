"use client";

export type ConfirmToolCallProps = {
  bookingId: string;
  onApprove: () => void;
  onReject: () => void;
};

/**
 * The confirmation card. It has to be accessible too - slide 40. Section B's
 * discipline does not stop at the seat map.
 */
export function ConfirmToolCall({ bookingId, onApprove, onReject }: ConfirmToolCallProps) {
  return (
    <div className="confirm" role="group" aria-labelledby="confirm-heading">
      <p id="confirm-heading" className="confirm__title">
        Cancel booking {bookingId}?
      </p>
      <p className="muted">This frees the seat for someone else. It cannot be undone.</p>
      <div className="confirm__actions">
        <button type="button" className="button" onClick={onApprove}>
          Confirm
        </button>
        <button type="button" className="button button--quiet" onClick={onReject}>
          Keep booking
        </button>
      </div>
    </div>
  );
}
