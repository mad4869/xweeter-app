const useFile = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const file = target.files?.[0];

    if (file) {
        const reader = new FileReader();

        return new Promise<string | undefined>((resolve) => {
            reader.onload = (e: ProgressEvent<FileReader>) => {
                if (e.target instanceof FileReader) {
                    const result = e.target.result as string;
                    resolve(result);
                } else {
                    resolve(undefined);
                }
            }
            reader.readAsDataURL(file)
        })
    }

    return Promise.resolve(undefined);
};

export default useFile;