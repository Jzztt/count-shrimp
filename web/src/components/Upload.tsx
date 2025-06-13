import React, { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Alert, AlertDescription, AlertTitle } from "./ui/alert";
import { motion, AnimatePresence } from "framer-motion";
import { FiUpload } from "react-icons/fi";
import { GiShrimp } from "react-icons/gi";
import {
  Dialog,
  DialogContent,
  DialogTrigger,
} from "@/components/ui/dialog";

const API_URL = "http://localhost:5000/process";

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setPreview(URL.createObjectURL(e.target.files[0]));
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (data.error) setError(data.error);
      else setResult(data);
    } catch (e) {
      setError("Lỗi kết nối API hoặc server không phản hồi.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white px-2">
      <Card className="w-full max-w-md bg-neutral-900 border border-neutral-800 shadow-xl">
        <CardHeader className="flex flex-col items-center gap-2">
          <GiShrimp className="text-4xl text-pink-400 mb-1" />
          <CardTitle className="text-2xl font-bold text-white tracking-tight">Shrimp Counter AI</CardTitle>
          <span className="text-xs text-neutral-400">Đếm tôm tự động từ ảnh</span>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-4">
            <label htmlFor="file-upload" className="flex flex-col items-center justify-center border-2 border-dashed border-neutral-700 rounded-lg p-4 cursor-pointer hover:border-pink-400 transition-colors">
              <FiUpload className="text-2xl mb-2 text-neutral-400" />
              <span className="text-neutral-400">Chọn ảnh để upload</span>
              <Input id="file-upload" type="file" accept="image/*" onChange={handleFileChange} className="hidden" />
            </label>
            <AnimatePresence>
              {preview && (
                <motion.div
                  key="preview"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 20 }}
                  transition={{ duration: 0.4 }}
                  className="flex justify-center"
                >
                  <img
                    src={preview}
                    alt="Preview"
                    className="rounded-lg shadow max-h-48 object-contain border border-neutral-800 bg-neutral-950"
                  />
                </motion.div>
              )}
            </AnimatePresence>
            <Button
              onClick={handleUpload}
              disabled={!file || loading}
              className="bg-pink-500 hover:bg-pink-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
            >
              {loading ? "Đang xử lý..." : "Upload Image"}
            </Button>
            {error && (
              <Alert variant="destructive">
                <AlertTitle>Lỗi</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
            <AnimatePresence>
              {result && (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 20 }}
                  transition={{ duration: 0.4 }}
                  className="mt-4 text-center"
                >
                  <div className="flex flex-col items-center gap-2">
                    <GiShrimp className="text-3xl text-pink-400" />
                    <div className="font-semibold text-xl text-white mb-2">Kết quả:</div>
                    <div className="mb-4 text-2xl text-white">
                      Số lượng tôm: <span className="font-bold text-pink-400">{result.count}</span>
                    </div>
                    {result.result_image && (
                      <Dialog>
                        <DialogTrigger asChild>
                          <img
                            src={`http://localhost:5000/static/${result.result_image}`}
                            alt="Kết quả"
                            className="rounded-lg shadow max-h-96 object-contain border border-neutral-800 bg-neutral-950 cursor-pointer hover:opacity-90 transition-opacity"
                          />
                        </DialogTrigger>
                        <DialogContent className="max-w-[90vw] max-h-[90vh] p-0 bg-neutral-900 border-neutral-800">
                          <img
                            src={`http://localhost:5000/static/${result.result_image}`}
                            alt="Kết quả"
                            className="w-full h-full object-contain"
                          />
                        </DialogContent>
                      </Dialog>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </CardContent>
      </Card>
      <footer className="mt-8 text-xs text-neutral-500 text-center opacity-70">
        &copy; {new Date().getFullYear()} Shrimp Counter AI. Made with <span className="text-pink-400">♥</span>
      </footer>
    </div>
  );
};

export default Upload; 