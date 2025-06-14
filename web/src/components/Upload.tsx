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
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { cn } from "@/lib/utils";

const API_URL = "http://localhost:5000/process";
const CLASSIC_API_URL = "http://localhost:5000/classic-process";

const UploadComponent: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setPreview(URL.createObjectURL(e.target.files[0]));
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async (method: 'roboflow' | 'traditional') => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await fetch(method === 'roboflow' ? API_URL : CLASSIC_API_URL, {
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

  // Tính toán dữ liệu cho trang hiện tại
  const getCurrentPageData = () => {
    if (!result?.features) return [];
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return result.features.slice(startIndex, endIndex);
  };

  // Tính toán tổng số trang
  const totalPages = result?.features ? Math.ceil(result.features.length / itemsPerPage) : 0;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white px-2">
      <Card className="w-[900px] bg-neutral-900 border border-neutral-800 shadow-xl">
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
            <div className="flex flex-col gap-2">
              <Button
                onClick={() => handleUpload('roboflow')}
                disabled={!file || loading}
                className="bg-pink-500 hover:bg-pink-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
              >
                {loading ? "Đang xử lý..." : "Đếm tôm (Roboflow)"}
              </Button>
              <Button
                onClick={() => handleUpload('traditional')}
                disabled={!file || loading}
                className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
              >
                {loading ? "Đang xử lý..." : "Đếm tôm (Phương pháp truyền thống)"}
              </Button>
            </div>
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
                    {result.features && (
                      <div className="w-full mb-4">
                        <h4 className="text-lg font-semibold mb-2 text-white">Thông số chi tiết:</h4>
                        <div className="rounded-md border border-neutral-800">
                          <Table>
                            <TableHeader>
                              <TableRow className="border-neutral-800">
                                <TableHead className="text-white">ID</TableHead>
                                <TableHead className="text-white">Diện tích</TableHead>
                                <TableHead className="text-white">Chu vi</TableHead>
                                <TableHead className="text-white">Độ tin cậy</TableHead>
                              </TableRow>
                            </TableHeader>
                            <TableBody>
                              {getCurrentPageData().map((feature: any) => (
                                <TableRow key={feature.id} className="border-neutral-800">
                                  <TableCell className="text-white">{feature.id}</TableCell>
                                  <TableCell className="text-white">{feature.area}</TableCell>
                                  <TableCell className="text-white">{feature.perimeter}</TableCell>
                                  <TableCell className="text-white">
                                    {feature.confidence ? `${(feature.confidence * 100).toFixed(2)}%` : 'N/A'}
                                  </TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </div>
                        {totalPages > 1 && (
                          <div className="mt-4 flex justify-center">
                            <Pagination>
                              <PaginationContent className="flex-wrap">
                                <PaginationItem>
                                  <PaginationPrevious 
                                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                                    className={cn(
                                      currentPage === 1 ? 'pointer-events-none opacity-50' : '',
                                      'text-white hover:text-white'
                                    )}
                                  />
                                </PaginationItem>
                                
                                {/* First page */}
                                <PaginationItem>
                                  <PaginationLink
                                    onClick={() => setCurrentPage(1)}
                                    isActive={currentPage === 1}
                                    className={cn(
                                      'text-white hover:text-white',
                                      currentPage === 1 ? 'bg-pink-500 hover:bg-pink-600' : 'hover:bg-neutral-800'
                                    )}
                                  >
                                    1
                                  </PaginationLink>
                                </PaginationItem>

                                {/* Left ellipsis */}
                                {currentPage > 3 && (
                                  <PaginationItem>
                                    <span className="px-4 text-white">...</span>
                                  </PaginationItem>
                                )}

                                {/* Current page and neighbors */}
                                {Array.from({ length: totalPages }, (_, i) => i + 1)
                                  .filter(page => {
                                    if (totalPages <= 5) return true;
                                    if (page === 1 || page === totalPages) return false;
                                    return Math.abs(currentPage - page) <= 1;
                                  })
                                  .map((page) => (
                                    <PaginationItem key={page}>
                                      <PaginationLink
                                        onClick={() => setCurrentPage(page)}
                                        isActive={currentPage === page}
                                        className={cn(
                                          'text-white hover:text-white',
                                          currentPage === page ? 'bg-pink-500 hover:bg-pink-600' : 'hover:bg-neutral-800'
                                        )}
                                      >
                                        {page}
                                      </PaginationLink>
                                    </PaginationItem>
                                  ))}

                                {/* Right ellipsis */}
                                {currentPage < totalPages - 2 && (
                                  <PaginationItem>
                                    <span className="px-4 text-white">...</span>
                                  </PaginationItem>
                                )}

                                {/* Last page */}
                                {totalPages > 1 && (
                                  <PaginationItem>
                                    <PaginationLink
                                      onClick={() => setCurrentPage(totalPages)}
                                      isActive={currentPage === totalPages}
                                      className={cn(
                                        'text-white hover:text-white',
                                        currentPage === totalPages ? 'bg-pink-500 hover:bg-pink-600' : 'hover:bg-neutral-800'
                                      )}
                                    >
                                      {totalPages}
                                    </PaginationLink>
                                  </PaginationItem>
                                )}

                                <PaginationItem>
                                  <PaginationNext
                                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                                    className={cn(
                                      currentPage === totalPages ? 'pointer-events-none opacity-50' : '',
                                      'text-white hover:text-white'
                                    )}
                                  />
                                </PaginationItem>
                              </PaginationContent>
                            </Pagination>
                          </div>
                        )}
                      </div>
                    )}
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

      <style jsx global>{`
        .custom-table .ant-table {
          background-color: #1f1f1f;
          color: white;
        }
        .custom-table .ant-table-thead > tr > th {
          background-color: #141414;
          color: white;
          border-bottom: 1px solid #303030;
        }
        .custom-table .ant-table-tbody > tr > td {
          background-color: #1f1f1f;
          color: white;
          border-bottom: 1px solid #303030;
        }
        .custom-table .ant-table-tbody > tr:hover > td {
          background-color: #2f2f2f;
        }
        .ant-pagination-item a {
          color: white;
        }
        .ant-pagination-item-active {
          background-color: #1890ff;
        }
        .ant-pagination-item-active a {
          color: white;
        }
        .ant-pagination-prev button,
        .ant-pagination-next button {
          color: white;
        }
      `}</style>
    </div>
  );
};

export default UploadComponent; 