if __name__ == "__main__":
    global args
    args, parser = parse(sys.argv[1:])
    try:
        if args.list_devices:
            print(sd.query_devices())
            parser.exit(0)

        # low level stream
        """
        callback (callable, optional) – User-supplied function to consume,
        process or generate audio data in response to requests from an active
        stream. When a stream is running, PortAudio calls the stream callback
        periodically. The callback function is responsible for processing and
        filling input and output buffers, respectively.

        If no callback is given, the stream will be opened in
        “blocking read/write” mode. In blocking mode, the client can receive
        sample data using read() and write sample data using write(), the
        number of frames that may be read or written without blocking is
        returned by read_available and write_available, respectively.

        The callback must have this signature:

        callback(indata: ndarray, outdata: ndarray, frames: int,
                time: CData, status: CallbackFlags) -> None
        The first and second argument are the input and output buffer,
        respectively, as two-dimensional numpy.ndarray with one column per
        channel (i.e. with a shape of (frames, channels)) and with a data type
        specified by dtype. The output buffer contains uninitialized data and
        the callback is supposed to fill it with proper audio data. If no data
        is available, the buffer should be filled with zeros
        (e.g. by using outdata.fill(0)).
        """
        print(args.device)
        stream = sd.InputStream(
            device=args.device,
            channels=args.channels,
            samplerate=args.samplerate,
            callback=audio_callback,
        )

        with stream:
            compute_pitch()
        # for d in range(len(args.device)):
        #     pitch_thread = threading.Thread(target=stream, args=(args, d))
        #     pitch_thread.start()

    except Exception as e:
        parser.exit(type(e).__name__ + ": " + str(e))
